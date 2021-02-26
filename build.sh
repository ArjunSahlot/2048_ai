#!/bin/bash

download_link=https://github.com/ArjunSahlot/2048_ai/archive/main.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/2048_ai-main $1/2048_ai \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/2048_ai[0m"
