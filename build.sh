#!/bin/bash

download_link=https://github.com/ArjunSahlot/2048_ai/archive/main.zip
temporary_dir=$(mktemp -d)
echo "Checking if curl is installed"
if [ $(dpkg-query -W -f='${Status}' curl3 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  echo -e "[0;31mcurl is not installed[0m"
  echo "Installing curl..."
  sudo apt install -y curl;
  echo -e "[0;32mcurl was successfully installed[0m"
else
  echo -e "[0;32mcurl is already installed[0m"
fi
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/2048_ai-main $1/2048_ai \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/2048_ai[0m"
echo "Checking if pip is installed"
if [ $(dpkg-query -W -f='${Status}' pip3 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  echo -e "[0;31mpip is not installed[0m"
  echo "Installing pip..."
  sudo apt install -y python3-pip;
  echo -e "[0;32mpip was successfully installed[0m"
else
  echo -e "[0;32mpip is already installed[0m"
fi
echo "Installing requirements"
cd $1/2048_ai
pip3 install -r requirements.txt
echo "[0;32mDone![0m"
