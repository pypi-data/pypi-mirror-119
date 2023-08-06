

BASEDIR=$(dirname $(dirname "$0"))

cd $BASEDIR/elasticsearch-7.9.2/

ES_JAVA_OPTS="\"-Xms256m -Xmx256m -XX:ErrorFile=$2/hs_err_pid%p.log -Xlog:gc*,gc+age=trace,safepoint:file=$2/gc.log:utctime,pid,tags:filecount=32,filesize=64m\""
cmd="ES_JAVA_OPTS=$ES_JAVA_OPTS ES_PATH_CONF=$3 JAVA_HOME=\"jre-15\" ES_DATA_PATH=\"$1\" ES_LOGS_PATH=\"$2\" ES_HTTP_PORT=\"$4\" ES_TRANSPORT_PORT=\"$5\" ./bin/elasticsearch"

echo $cmd
eval "$cmd"