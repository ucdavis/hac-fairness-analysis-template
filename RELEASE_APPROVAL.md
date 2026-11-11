# Publication code release record

Status: **PRE-RELEASE**

Use this short record before formally citing, archiving, or announcing the code. It is for
group-created analysis code supporting a scholarly publication, not a clinical software
release or legal review.

## 1. Publication

- Repository: `ucdavis/hac-fairness-analysis-template`
- Manuscript: *From Performance Metrics to Patient Consequences: A Framework for Assessing Fairness in Clinical Prediction Models*
- Corresponding author:
- Target journal or venue:
- Repository coordinator: Yunyi Ren
- Review date: 2026-11-10

## 2. Contributors and permissions

List the people who wrote copyrightable code or documentation. This list may differ from the
manuscript author list.

| Contributor | Verified UC Davis position | Project contribution | Publication approval |
| --- | --- | --- | --- |
| Yunyi Ren, M.S. | Senior Statistician, CTSC | Initial repository and analysis code | Pending confirmation |
| Sandra Taylor, Ph.D. | CTSC Biostatistics Program Manager; Principal Biostatistician | To confirm | Pending confirmation |

Public affiliation source: [UC Davis CTSC Biostatistics team](https://health.ucdavis.edu/ctsc/area/biostatistics/biostatistics-team)

Confirm all of the following:

- [ ] Every code contributor is listed and approves public posting and the citation metadata.
- [x] The code is scholarly analysis material, not a separately required software deliverable.
- [ ] No contributor's employment duties create an unresolved ownership question.
- [ ] No grant, contract, data-use agreement, or collaborator restricts the release.
- [x] Repository review found no copied third-party code, confidential information, credentials, PHI, or patient data.
- [x] No UC Davis logo is included; the UC Davis name is used for affiliation and attribution.

Select one:

- [ ] **Group approval:** all statements above are confirmed; the contributors approve publication.
- [x] **UC review needed:** both contributors hold UC Davis staff positions, so confirm authority for public distribution of work created within employment duties.

Approval evidence or internal reference: Contributor consent and funding/agreement review pending.
See [UC Davis copyright guidance](https://research.ucdavis.edu/research-support/technology-transfer/copyrights/).

## 3. Group release approval

If **Group approval** was selected above, record the group sign-off here. Written agreement by
email or in group records is sufficient for this record: code contributors approve public
posting and citation metadata, and the corresponding author, PI, or project lead approves the
publication release. Seek UC review when ownership or distribution authority is uncertain.

- Reuse license: None — no open-source or other reuse license is granted
- Copyright notice: Default copyright applies; rights remain with the applicable owner or owners
- Publication commit or version tag:
- Archive DOI, if used:

Final checks:

- [x] Synthetic-data tests pass (`python -m unittest discover -s tests -v`: 4 passed on 2026-11-10).
- [x] `LICENSE-NOTICE.md` states that no reuse license is granted.
- [x] README and `CITATION.cff` contain software citation information.
- [ ] Notebook outputs and Git history contain no sensitive material.

- Group approver (corresponding author, PI, or project lead): Pending
- Repository maintainer: Yunyi Ren
- Approval date:
- UC approval reference, only if **UC review needed** was selected: Pending

If any ownership or agreement answer is uncertain, pause the license decision and ask the
appropriate UC Davis copyright or technology-transfer contact. Otherwise, this completed
record is the group's lightweight release documentation.
