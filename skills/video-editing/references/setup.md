# Setup and packaging

This lightweight entrypoint belongs in the shipped `skills/` catalog so an
ordinary request such as “EVE, lass uns Videos schneiden” discovers it. The
editor dependency is installed only on an appropriate editing host. A skill
file does not install Final Cut or turn a cloud container into the user's Mac.

## Reuse the existing setup owners

1. Check connected capabilities with `tool_search`; keep an existing working
   editor connection. The expected default name is `fcpxml`.
2. Resolve the computer that owns the project/media. For a local Hermes runtime
   on the Mac, stdio can run the MCP directly. Cloud Hermes needs the product's
   authenticated local-tool transport. Verify that transport first; do not
   expose an unauthenticated port or point cloud `localhost` at the user's Mac.
3. Use a dedicated Python environment for the pinned FCPXML MCP. Its package
   contains top-level `server` and `tools` modules which must not shadow Hermes
   modules. The example uses Python's isolated `-I` mode.
4. Add one MCP entry through the existing per-profile setup UI/CLI. The example
   is a template, not a command that should overwrite the full MCP map.
5. Set an explicit nonempty `FCP_PROJECTS_DIRS` to the authorized media roots.
   Set the journal/cache paths deliberately. User content belongs in a selected
   project, not the application's installation directory.

`examples/hermes-mcp.json` shows the native Hermes configuration shape. Replace
its paths with real existing directories on the tool's host. Keep credentials
out of this file. Generated-video credentials belong to the existing provider
configuration, not the Final Cut MCP.

## Rollout boundary

Package the skill in the runtime/distribution used by EVE, including cloud
workspaces. Installing a desktop client alone does not update a remote agent's
skills. Reuse normal skill seeding/synchronization for new and existing profiles;
do not overwrite user-edited skills, SOUL or memory. Respect native cache-aware
session refresh and prove discovery in the user's actual EVE conversation.

Final Cut/MCP setup, generated-video accounts and the Live conversation are
separate capabilities. Surface their actual readiness, then prepare the next
allowed step. Missing Final Cut should lead to a useful setup conversation, not
an invented claim that editing has started.

## Managed EVE customers

Customers should not need Cloudflare accounts, developer API keys or a manual
R2 configuration to use EVE's managed video-generation path. Resolve the existing
EVE authenticated media-upload, private-storage, presigned-read and billing
owners first. The desktop sends only the selected reference range through that
path; the backend supplies a short-lived media URL to the provider and returns
the job/result to the same customer workspace. Keep provider/storage credentials
server-side and retain existing user/workspace isolation and product permissions.

The pilot's developer-side Rclone connection is evidence of transport only,
not a customer installation mechanism. If the managed upload/presign capability
is absent, it is a release integration gap. Wire the smallest adapter at the
existing media owner; do not ask every customer to recreate the developer setup
or treat this skill file as implementation of that service. Verify with a fresh
account without developer credentials before claiming the feature is bundled.

## Source and dependency

- FCPXML MCP: https://github.com/DareDev256/fcp-mcp-server — MIT.
- Tested package target: `fcp-mcp-server==0.25.0`.
- Wheel SHA256: `7e34126c8561a6ba634bbd51ce53513ae930c995ee48d55674a5a2f83f4a605a`.
- `requirements-tested.txt` records the dependency set used with Python 3.14.5
  on macOS. Revalidate it on other supported platforms/Python versions and after
  updates; this snapshot is not a universal customer installation certification.
- `FCP_PROJECTS_DIRS` scopes reads. The similarly named legacy singular setting
  is only the listing preference in this package.

SpliceKit is an alternative for deeper in-app editing, not an implicit dependency:
https://github.com/elliotttate/SpliceKit. Its patched-app path needs separate
compatibility and installation acceptance.
