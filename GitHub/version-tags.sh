#!/bin/bash

git show-ref --tags | while read sha ref
do
  version=${ref#refs/tags/v}
  echo $version
  # git tag -d v${version}
done

for x in 3;
do
  for y in 0;
  do
    for z in `seq 1 9`;
    do
      tag=$x.$y.$z
      git tag -d v$tag
      git push origin :refs/tags/v$tag
    done
  done
done
