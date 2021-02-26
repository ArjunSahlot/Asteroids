#!/bin/bash

download_link=https://github.com/ArjunSahlot/asteroids/archive/master.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir master.zip \
&& rm -rf master.zip \
&& mv $temporary_dir/asteroids-master $1/asteroids \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/asteroids[0m"
