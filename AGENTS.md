Fleet canon: `fleet-canon` v3 at https://github.com/JackReis/vault-fleet/blob/canon-v3/canon/fleet-canon.md (private repo). Each host resolves its local copy as `$VAULT_ROOT/canon/fleet-canon.md` from `~/.fleet/hosts.env`.

## Change Verification

Before changing code, trace direct callers and imports in source and assess affected behavior. Surface material risks before proceeding. Before committing, inspect the diff for unintended changes and run the relevant normal tests and checks.

GitNexus is optional, only when explicitly requested; it is not an editing or commit prerequisite. Do not run it or reindex automatically.
