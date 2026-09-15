from pathlib import Path
import argparse, array, hashlib, json, math, subprocess, sys

parser = argparse.ArgumentParser(description='Reproduce the 2026-09-15 local assembler probes. No API calls.')
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
parser.add_argument('--output', type=Path, required=True, help='New output directory; existing files are never removed.')
parser.add_argument('--pilot', type=Path, help='Optional local 20-90s pilot for technical validator scope check.')
args = parser.parse_args()
ROOT = args.output.resolve()
ROOT.mkdir(parents=True, exist_ok=False)
FIX = ROOT / 'fixtures'
FIX.mkdir()
SOURCE = args.repo.resolve()
ASSEMBLER = SOURCE / 'skills/produce-brand-film/scripts/assemble_film.py'
VALIDATOR = SOURCE / 'skills/produce-brand-film/scripts/validate_film.py'
MASTER = args.pilot.resolve() if args.pilot else None

def run(args):
    return subprocess.run(args, text=True, capture_output=True, check=True)

def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size:stream=codec_type,duration', '-of', 'json', str(path)]).stdout)

def rms(path):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0', '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'])
    values = array.array('f', raw)
    return math.sqrt(sum(x*x for x in values)/len(values))

run(['ffmpeg','-v','error','-n','-f','lavfi','-i','testsrc2=size=320x180:rate=24','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','2','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ac','2',str(FIX/'source.mp4')])
run(['ffmpeg','-v','error','-n','-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','2','-ac','2',str(FIX/'voice.wav')])
run(['ffmpeg','-v','error','-n','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','2',str(FIX/'silence.wav')])

results = {'reviewed_commit':run(['git','-C',str(SOURCE),'rev-parse','HEAD']).stdout.strip(), 'scope':'local synthetic probes of existing helpers; not film-quality tests', 'observations':[]}
outputs={}
for name,duration,audio in [
    ('source-audio',2,{}),
    ('short-source',4,{}),
    ('voice-one',2,{'voice':str(FIX/'voice.wav'),'voice_volume':1}),
    ('voice-zero',2,{'voice':str(FIX/'voice.wav'),'voice_volume':0}),
    ('voice-silent-music',2,{'voice':str(FIX/'voice.wav'),'voice_volume':1,'music':str(FIX/'silence.wav'),'music_volume':1}),
]:
    output=FIX/(name+'.mp4');work=FIX/(name+'-work')
    m={'width':320,'height':180,'fps':24,'output':str(output),'scenes':[{'source':str(FIX/'source.mp4'),'duration':duration}],'audio':audio}
    spec=FIX/(name+'.json');spec.write_text(json.dumps(m,indent=2)+'\n')
    process=run([sys.executable,str(ASSEMBLER),'--manifest',str(spec),'--work-dir',str(work)])
    (FIX/(name+'-stdout.txt')).write_text(process.stdout)
    outputs[name]={'requested_duration':duration,'reported_duration':json.loads(process.stdout)['duration_seconds'],'exit_code':process.returncode,'media':probe(output),'rms':rms(output),'normalized_streams':probe(work/'scene-00.mp4')['streams']}
    print(name,json.dumps(outputs[name]),flush=True)

results['observations'].append({'id':'source_audio','input_rms':rms(FIX/'source.mp4'),'result':outputs['source-audio'],'interpretation':'Source soundtrack is removed and final output receives a silent track when no separate voice/music is supplied.'})
results['observations'].append({'id':'short_source','input_duration':probe(FIX/'source.mp4')['format']['duration'],'result':outputs['short-source'],'interpretation':'Declared usable range exceeds source; inspect actual stream durations against declared output.'})
results['observations'].append({'id':'voice_volume','gain_1_rms':outputs['voice-one']['rms'],'gain_0_rms':outputs['voice-zero']['rms'],'rms_ratio':outputs['voice-zero']['rms']/outputs['voice-one']['rms'],'interpretation':'Voice-only path does not apply voice_volume=0.'})
results['observations'].append({'id':'mix_normalization','voice_only_rms':outputs['voice-one']['rms'],'with_silent_music_rms':outputs['voice-silent-music']['rms'],'rms_ratio':outputs['voice-silent-music']['rms']/outputs['voice-one']['rms'],'interpretation':'Adding a silent music input changes level at unchanged voice gain.'})
if MASTER is not None:
    vp=subprocess.run([sys.executable,str(VALIDATOR),str(MASTER),'--json-out',str(ROOT/'master-technical-validation.json')],capture_output=True,text=True)
    v=json.loads((ROOT/'master-technical-validation.json').read_text())
    results['observations'].append({'id':'technical_validator_scope','master_sha256':hashlib.sha256(MASTER.read_bytes()).hexdigest(),'exit_code':vp.returncode,'verdict':v['verdict'],'checks':v['checks'],'interpretation':'Format/decode result only; this artifact has a separately reported human-observed cross-cut speech defect.'})
results['tools']={'python':sys.version.split()[0],'ffmpeg':run(['ffmpeg','-version']).stdout.splitlines()[0]}
(ROOT/'local-probes.json').write_text(json.dumps(results,indent=2)+'\n')
print('PROBES_COMPLETE',flush=True)
