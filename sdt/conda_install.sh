#!/usr/bin/env bash

conda create -y -c defaults -c conda-forge --override-channels -n sdt python=2 pyOpenSSL=17.5 psutil humanize tabulate progress json-rpc python-daemon retrying requests beautifulsoup4 texttable pillow reportlab myproxyclient
source activate sdt
pip install pycountry

CONDA_ROOT=`conda info --base`
SDT_ENV="${CONDA_ROOT}/envs/sdt"
SDT_LIB="${SDT_ENV}/lib/sd"
SDT_CONF_FILE="${SDT_ENV}/conf/sdt.conf"
SDT_CRED_FILE="${SDT_ENV}/conf/credentials.conf"

python setup.py install --install-scripts=${SDT_LIB}

chmod go+r "$SDT_CONF_FILE"
chmod u=rw,g=,o= "$SDT_CRED_FILE"

# create symlinks in 'bin'
cd ${SDT_ENV}/bin
ln -fs ${SDT_LIB}/sdcleanup_tree.sh sdcleanup_tree.sh
ln -fs ${SDT_LIB}/sdget.sh sdget.sh
ln -fs ${SDT_LIB}/sdgetg.sh sdgetg.sh
ln -fs ${SDT_LIB}/sdlogon.sh sdlogon.sh
ln -fs ${SDT_LIB}/sdparsewgetoutput.sh sdparsewgetoutput.sh
ln -fs ${SDT_LIB}/synda_cmd.py synda
ln -fs ${SDT_LIB}/sdtc.py sdtc
ln -fs ${SDT_LIB}/sdconfig.py sdconfig
ln -fs ${SDT_LIB}/sdget.py sdget
ln -fs ${SDT_LIB}/sdmerge.py sdmerge
ln -fs ${SDT_LIB}/sddownloadtest.py sddownloadtest

# Perform any necessary updates
export ST_HOME=${SDT_ENV}
$SDT_ENV/bin/synda update

echo "Install complete."
echo "To use, load SDT environment: source activate sdt"
echo "Add ST_HOME variable to your environment."
echo "export ST_HOME=${SDT_ENV}"
