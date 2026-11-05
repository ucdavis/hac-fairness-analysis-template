# Public release checklist

Complete this checklist before making the repository public.

## Authorization and attribution

- [ ] Confirm the copyright owner and all software contributors.
- [ ] Obtain approval from the appropriate UC Davis delegated licensing or copyright authority.
- [ ] Replace `LICENSE-NOTICE.md` with the approved `LICENSE` file and update the README.
- [ ] Confirm that the UC Davis Health name and any branding are approved for this use.
- [ ] Add the final manuscript author list, year, journal, DOI, and `CITATION.cff` metadata when available.
- [ ] Identify a repository maintainer or approved contact channel.

## Privacy and security

- [ ] Review every staged file with `git status` and `git diff --cached`.
- [ ] Confirm that no PHI, PII, patient-level data, credentials, private URLs, local paths, or sensitive output are present.
- [ ] Confirm that example data, if added later, are synthetic or explicitly approved for public release.
- [ ] Confirm that notebook outputs are intentionally cleared or approved for publication.

## Reproducibility and quality

- [ ] Run the notebook from a clean environment using `requirements.txt`.
- [ ] Test each advertised input format that the project intends to support.
- [ ] Review threshold, resampling, minimum-group-size, and subgroup defaults.
- [ ] Confirm that methodological limitations and intended use are accurate.
- [ ] Confirm that the forthcoming manuscript description is current.

## GitHub release

- [ ] Use a `main` default branch.
- [ ] Add a concise GitHub repository description and relevant topics.
- [ ] Decide whether Issues and Discussions should be enabled.
- [ ] Add branch protection or required review rules if multiple maintainers will contribute.
- [ ] Create a versioned release after the initial public commit is reviewed.
