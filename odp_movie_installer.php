<?php
/**
  * Author: chenchiyuan@baidu.com
  */

$INSTALL_PATH = "/home/map/odp_movie"; # 安装目录，没有反斜杠结尾
$ODP_SH_PATH="/home/map/install_odp/"; # ODP安装脚本路径
$AIM_SERVER = "cq02-map-detail01.cq02.baidu.com";  # 线上机器，提供当前最新代码

function install_odp(){
    global $ODP_SH_PATH, $INSTALL_PATH;
    $install_command = "cd {$ODP_SH_PATH} && ./install_odp.sh -d={$INSTALL_PATH} -s=nginx -t=develop";
    echo __METHOD__ . "\t exec: " . $install_command . "\n" ;
    exec($install_command);
}

function download_app(){
    global $INSTALL_PATH, $AIM_SERVER;
    $server_path = "/home/map/odp_movie/";
    $download_dirs = array(
        "app",
        "conf",
        "data",
        "php/phplib/movie",
        "php/phplib/ext/smarty",
        "template",
        "webroot",
        "webserver/conf",
        "php/lib/php/extensions/no-debug-non-zts-20060613/redis.so"
    );
    $download_command = "wget -nH --cut-dirs=3 --limit-rate=18m -r -l 20 -N ftp://{$AIM_SERVER}";
    foreach($download_dirs as $dir){
        $command = "{$INSTALL_PATH}/{$dir}";
        echo $command . "\n";
        exec($command);
    }
    foreach($download_dirs as $dir){
        $command = "cd {$INSTALL_PATH} && {$download_command}{$server_path}{$dir}";
        echo __METHOD__ . "\t exec: " . $command;
        exec($command);
    }
}

function replace_conf(){
    global $INSTALL_PATH;
    $replace_conf_dir = array("/conf/app/info", "/conf/app/ticket", "webserver/conf/vhost");
    $from = str_replace("/", "\/", "/home/map/odp_movie");
    $to = str_replace("/", "\/", $INSTALL_PATH);
    foreach($replace_conf_dir as $dir){
        $replace_command = "'s/{$from}/{$to}/g'";
        $command = "cd {$INSTALL_PATH}/{$dir} && find . -name '*.conf' | xargs sed -i " . $replace_command;
        echo __METHOD__ . "\t exec: " . $command . "\n";
        exec($command);
    }
}

function process(){
    install_odp();
    download_app();
    replace_conf();
}

process();