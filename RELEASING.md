# 🚀 Releasing Context Packer

## Prerequisites

1. **PyPI Account**: Create at [pypi.org](https://pypi.org)
2. **API Token**: Get from [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
3. **Configure Token** (choose one):
   - **Option A**: Set environment variables
     ```bash
     export TWINE_USERNAME=__token__
     export TWINE_PASSWORD=pypi-YOUR-TOKEN-HERE
     ```
   - **Option B**: Create `~/.pypirc` (see `.pypirc.example`)

## 🎯 One-Command Release

### Fastest Method
```bash
# Patch release (1.0.0 -> 1.0.1)
python release.py

# Minor release (1.0.0 -> 1.1.0)
python release.py minor

# Major release (1.0.0 -> 2.0.0)
python release.py major
```

### Alternative: Make Command
```bash
# Using Makefile
make release                # patch
make release VERSION=minor   # minor
make release VERSION=major   # major
```

### Alternative: Shell Script
```bash
# Using bash script
./quick-release.sh         # patch
./quick-release.sh minor   # minor
./quick-release.sh major   # major
```

## What Happens

The release script automatically:
1. ✅ Runs tests
2. 🎨 Formats code
3. 📝 Bumps version
4. 📌 Commits changes
5. 🏷️ Creates git tag
6. 🚀 Pushes to GitHub
7. 📦 Builds package
8. 🌍 Publishes to PyPI
9. 🎉 Creates GitHub release (via Actions)

## Manual Release (if needed)

```bash
# 1. Bump version
python bump_version.py patch

# 2. Commit and tag
git add -A
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z

# 3. Push
git push origin main --tags

# 4. Build and publish
python -m build
twine upload dist/*
```

## Troubleshooting

### Authentication Error
```bash
# Check token is set
echo $TWINE_PASSWORD

# Or check ~/.pypirc exists
cat ~/.pypirc
```

### Build Error
```bash
# Install build tools
pip install --upgrade build twine
```

### Git Push Error
```bash
# Make sure you're on main branch
git checkout main
git pull origin main
```

## Version Strategy

- **Patch** (x.y.Z): Bug fixes, minor updates
- **Minor** (x.Y.z): New features, backwards compatible
- **Major** (X.y.z): Breaking changes

## 📅 Release Checklist

- [ ] All tests passing
- [ ] README updated if needed
- [ ] No uncommitted changes
- [ ] On main branch
- [ ] PyPI token configured

---

💡 **Tip**: Use `python release.py` for the smoothest experience!