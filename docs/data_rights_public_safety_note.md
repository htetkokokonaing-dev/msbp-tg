# Public data-rights cleanup note ()

Step 2 removes row-level third-party-derived representative case tables from the public repository and replaces the representative-structure figure with synthetic illustrative motifs.

The package now distinguishes three categories:

1. **Allowed in public repo:** aggregate statistics, source-role notes, source manifests, scripts, figures, manuscript text, and license/audit notes.
2. **Not bundled:** raw third-party datasets, processed third-party row tables, and row-level SMILES/Tg records.
3. **Requires future explicit audit:** any file that combines structural identifiers (`SMILES`, `canonical_smiles`, etc.) with Tg-like target fields (`Tg`, `Tg_C`, `Tg_value_raw`, etc.).

The public-safe checker now fails on suspicious CSV headers that combine structural identifier fields with Tg-like target fields.
