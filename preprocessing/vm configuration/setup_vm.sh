#!/bin/bash

echo "🚀 Starting VM setup for Data Engineering Project..."

# Update system and install necessary utilities
echo "🔄 Updating system packages..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y wget curl unzip tar git software-properties-common 
nano

# Install Java (required for Hadoop & Spark)
echo "☕ Installing Java..."
sudo apt install -y openjdk-11-jdk
echo "JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))" | sudo 
tee -a /etc/environment
source /etc/environment

# Install Hadoop
echo "📂 Installing Hadoop..."
wget 
https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xvzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /usr/local/hadoop
rm hadoop-3.3.6.tar.gz

# Set up Hadoop environment variables
echo "🔧 Configuring Hadoop..."
echo "export HADOOP_HOME=/usr/local/hadoop" | sudo tee -a ~/.bashrc
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" | sudo tee 
-a ~/.bashrc
source ~/.bashrc

# Install Spark
echo " Installing Spark..."
wget 
https://downloads.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz
tar -xvzf spark-3.4.1-bin-hadoop3.tgz
sudo mv spark-3.4.1-bin-hadoop3 /usr/local/spark
rm spark-3.4.1-bin-hadoop3.tgz

# Set up Spark environment variables
echo " Configuring Spark..."
echo "export SPARK_HOME=/usr/local/spark" | sudo tee -a ~/.bashrc
echo "export PATH=\$PATH:\$SPARK_HOME/bin:\$SPARK_HOME/sbin" | sudo tee -a 
~/.bashrc
source ~/.bashrc

# Install Python, Pip & Jupyter Notebook
echo " Installing Python, Pip & Jupyter Notebook..."
sudo apt install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install jupyterlab notebook jupyter

# Install NLTK for sentiment analysis
echo " Installing NLTK & dependencies..."
pip3 install nltk
python3 -m nltk.downloader all

# Install PySpark & dependencies
echo " Installing PySpark..."
pip3 install pyspark pandas numpy

# Install SSH for HDFS & Spark communication
echo " Setting up SSH..."
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh

# Start Jupyter Notebook server
echo " Configuring Jupyter Notebook..."
mkdir -p ~/.jupyter
echo "c.NotebookApp.ip = '0.0.0.0'" >> 
~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> 
~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py

# Final message
echo " Setup complete! You can now run Hadoop, Spark & Jupyter 
Notebook."
echo "️ Start Jupyter Notebook: jupyter notebook --ip=0.0.0.0 --port=8888 
--no-browser"
echo "️ Start Spark: /usr/local/spark/bin/pyspark"
echo "️ Start Hadoop: /usr/local/hadoop/bin/hdfs namenode -format"

echo " Everything is installed!"

