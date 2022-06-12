





## Download Java

```bash

# cd into tmp folder
    cd /

# download
    wget https://download.java.net/java/ga/jdk11/openjdk-11_linux-x64_bin.tar.gz

# extract tar
    tar xzvf openjdk-11_linux-x64_bin.tar.gz -C ~/spark 
```

If you downloaded it into `/tmp` don't worry about deleting it.

## Add java to PATH

```bash

# export JAVA_HOME
    export JAVA_HOME="${HOME}/spark/jdk-11"

# add JAVA_HOME to PATH
    export PATH="${JAVA_HOME}/bin:${PATH}"

# check that it worked
    which java
```

## Install spark

Same commands as the java above

```bash

# cd into tmp folder
    cd /

# download
    wget https://dlcdn.apache.org/spark/spark-3.0.3/spark-3.0.3-bin-hadoop3.2.tgz

# extract tar into spark folder
    tar xzvf spark-3.0.3-bin-hadoop3.2.tgz -C ~/spark 
```

## Add java to PATH

```bash

# export SPARK_HOME
    export SPARK_HOME="${HOME}/spark/spark-3.0.3-bin-hadoop3.2"

# add SPARK_HOME to PATH
    export PATH="${SPARK_HOME}/bin:${PATH}"
```

```scala

// check that it worked
// ignore the many warnings;)
    spark-shell

// scala code to test spark
    val data = 1 to 10000
    val distData = sc.parallelize(data)
    distData.filter(_ < 10).collect()
```

# Update .bashrc file

Add the export commands to the .bashrc file so each time you start you making you PATH with be correct with do all that export.

Open .bashrc with editor and paste export commands at the bottom.

```bash

# open editor, can use nano as well
vim ~/.bashrc

# export JAVA_HOME
export JAVA_HOME="${HOME}/spark/jdk-11"

# add JAVA_HOME to PATH
export PATH="${JAVA_HOME}/bin:${PATH}"

# export SPARK_HOME
export SPARK_HOME="${HOME}/spark/spark-3.0.3-bin-hadoop3.2"

# add SPARK_HOME to PATH
export PATH="${SPARK_HOME}/bin:${PATH}"
```

Source .bashrc and check if PATH is right.

```bash

source ~./bashrc
which java
which pyspark
```

you may get asked for a token or login if you click the local button in the ports seection of vscode.  In ther terminal out put there is a link which contains the token.  Probably easier to just copy the enite link and open the locahost via compying an pasting.

http://localhost:8888/?token=
