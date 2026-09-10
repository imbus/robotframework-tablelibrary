#!/usr/bin/env bash
set -e

# Script takes one argument: e.g. 0.1.0 or 1.0.0
if [ -z "$1" ]; then
  echo "❌ Usage: $0 <new_version>"
  exit 1
fi

NEW_VERSION="$1"
TAG="v${NEW_VERSION}"

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "❌ Tag '${TAG}' already exists locally."
  exit 1
fi

if git ls-remote --exit-code --tags origin "refs/tags/${TAG}" >/dev/null 2>&1; then
  echo "❌ Tag '${TAG}' already exists on origin."
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Working tree has uncommitted changes. Commit or stash them before creating a release."
  exit 1
fi

echo "🏷️ Creating '${TAG}' on the current commit"
git tag -a "$TAG" -m "Release ${TAG}"
git push origin "$TAG"

echo "✅ Tag '${TAG}' created and pushed. GitHub Actions will build and publish the release."
