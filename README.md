# Ariful Islam Portfolio

A separate copy of Ariful Islam Fahim’s portfolio with the approved mint/Poppins design. The older `arif-portfolio-studio` repository remains independent.

## Edit without code

Use [Pages CMS](https://app.pagescms.org/) and select **arifulislamfahim04 → ariful-islam-portfolio → main**. The editor reads `.pages.yml`. See [EDITING.md](EDITING.md) for the content fields and [CMS_QUICK_START.md](CMS_QUICK_START.md) for a first edit.

Saving content commits it to this repository. GitHub Actions builds and publishes it; changes do not affect the old site.

## Build and publish

GitHub Settings → Pages must use **GitHub Actions**. The `Publish portfolio content` workflow builds `docs/` from `editor/`, `templates/` and `scripts/`. Media lives in `docs/assets/`.

```sh
python -m pip install -r requirements.txt
python scripts/build_editor.py
python scripts/check_site.py
python scripts/test_launch.py
```

Edit source files, then rebuild. Do not edit generated HTML alone. `dist/` is a legacy input; do not overwrite it with `docs/`. No frontend tokens or paid backend are needed. The contact form prepares email drafts; it does not send messages itself.

The public repository and media are visible even when a CMS entry is unpublished. Keep confidential drafts and documents elsewhere. Existing attribution and asset notices remain in the project.
