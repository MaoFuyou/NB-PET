# Release status

| Component | Included in this repository? | Release boundary |
|---|---|---|
| Project overview and documentation | Yes | Overview of the research method. |
| Manuscript Figures 1 and 4 and Table 3 | Yes | [Selected manuscript results](paper-results.md); no downloadable case series or case-level data. |
| Synthetic scoring example and tests | Yes | No patient data or trained model; documentation and scoring demonstration only. |
| Full preprocessing, training, and model inference | No | Needs an allowlisted export, documented dependencies, and a clean-machine smoke test. |
| Model checkpoints | No | Review model ownership, dependencies, redistribution terms, and permitted uses. |
| Patient scans, reports, splits, and prediction files | No | Do not commit or attach to issues or releases. |
| Paper link, citation file, and license | No | Add only once the corresponding publication metadata and terms are approved. |

## Release checklist

1. Confirm the repository owner, project name, visibility, and who may approve a release.
2. Reconcile the manuscript tables and README claims. Never substitute raw runs or draft metrics for approved results.
3. Export only approved modules and data-free configuration from the research project. Review each included dependency and any pretrained weights separately.
4. Test in a clean environment. Review the file list and Git history for credentials, identifying filenames, scans, reports, and case-level outputs.
5. Add the approved license and citation metadata. Tag a release only after the corresponding paper and code version have been checked.

Do not advertise access to a full implementation, clinical dataset, paper PDF, or checkpoints until those artifacts have been explicitly approved and are actually available.
