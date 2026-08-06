#!/bin/zsh
set -e

ROOT="/Users/xiaodongwang/Documents/pptprofilo/do/Myblogs/Myblogs"

hugo --source "$ROOT" --destination "$ROOT/public"
