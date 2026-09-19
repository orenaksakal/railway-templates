#!/bin/sh
# Seed only a missing directory, using a same-volume atomic rename.
# Existing directories (even empty ones) always belong to the operator.
seed_dir() {
  source_dir=$1
  destination_dir=$2
  if [ ! -d "$destination_dir" ]; then
    parent_dir=$(dirname "$destination_dir")
    mkdir -p "$parent_dir"
    staging_dir=$(mktemp -d "$parent_dir/.seed.XXXXXX")
    if [ -d "$source_dir" ]; then
      cp -a "$source_dir/." "$staging_dir/" || { rm -rf "$staging_dir"; return 1; }
    fi
    mv "$staging_dir" "$destination_dir"
  fi
}
