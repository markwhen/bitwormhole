document.getElementById("jump2another").setAttribute("onclick","jump()");

document.getElementById("another").setAttribute("onkeydown","enterjump()");

function jump(){
	$name = document.getElementById("another").value;
	if ( $name.length>0 )
		window.location.href='http://bitwormhole.com/'+$name;
}
function enterjump(){
	var event = window.event || arguments.callee.caller.arguments[0];
	if (event.keyCode == 13)
	{
		jump();
	}
}

/******check keyword*******/
function isPassword(){
    var str = document.getElementById("keyword").value.trim();
    if(str.length!=0){
        var reg = /^[0-9A-Za-z]+$/;
        var r = str.match(reg);
        if(r){
		document.getElementById("keywordinfo").innerHTML="OK";
	}else{
		document.getElementById("keyword").value = "OK";
		alert("only 0-9 a-z A-Z is ok");
		document.getElementById("keywordinfo").innerHTML="<p class='help-block'>only 0-9 a-z A-Z is ok</p>";
        }
    }
}

document.getElementById("keyword").setAttribute("onchange","isPassword()");

/******md5 keyword on submit*********/
function onUpload(){
	var str = document.getElementById("keyword").value.trim();
	str_md5 = hex_md5(str);
	str_md5 = str_md5.substring(0,16);
	document.getElementById("keyword").value = str_md5;
}

/*********************************upload file**************************************/
// common variables
var iBytesUploaded = 0;
var iBytesTotal = 0;
var iPreviousBytesLoaded = 0;
var iMaxFilesize = 1024*1024*1024;
var oTimer = 0;
var sResultFileSize = '';

function secondsToTime(secs) { // we will use this function to convert seconds in normal time format
    var hr = Math.floor(secs / 3600);
    var min = Math.floor((secs - (hr * 3600))/60);
    var sec = Math.floor(secs - (hr * 3600) -  (min * 60));

    if (hr < 10) {hr = "0" + hr; }
    if (min < 10) {min = "0" + min;}
    if (sec < 10) {sec = "0" + sec;}
    if (hr) {hr = "00";}
    return hr + ':' + min + ':' + sec;
};

function bytesToSize(bytes) {
    var sizes = ['Bytes', 'KB', 'MB'];
    if (bytes == 0) return 'n/a';
    var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
};

function fileSelected() {

    // get selected file element
    var oFile = document.getElementById('file').files[0];

    // little test for filesize
    if (oFile.size > iMaxFilesize) {
        document.getElementById('file_notice').innerHTML = "文件大小超过了限制";
        return;
    }
    if (oFile.size < 1) {
        document.getElementById('file_notice').innerHTML = "你忘记选择文件了";
    }

    // prepare HTML5 FileReader
    var oReader = new FileReader();
    
    // read selected file as DataURL
    oReader.readAsDataURL(oFile);
}

function startUploading() {
     var oFile = document.getElementById('file').files[0];
    // little test for filesize
    if (oFile.size > iMaxFilesize) {
        alert("文件大小超过了限制");
        document.getElementById('file_notice').innerHTML = "文件大小超过了限制";
        return;
    }
    if (oFile.size < 1) {
        document.getElementById('file_notice').innerHTML = "你忘记选择文件了";
        alert("您忘记了选择文件");
        return;
    }
    if (oFile.name.length>70){
        alert("文件名太长，应小于70字符");
        return;
    }
    // cleanup all temp states
    iPreviousBytesLoaded = 0;
    document.getElementById('progress_percent').innerHTML = '';
    var oProgress = document.getElementById('progress');
    oProgress.style.display = 'block';
    oProgress.style.width = '0px';
    document.getElementById('file_notice').innerHTML = '';
    onUpload();
    // get form data for POSTing
    //var vFD = document.getElementById('upload_form').getFormData(); // for FF3
    var vFD = new FormData(document.getElementById('upload_form')); 

    // create XMLHttpRequest object, adding few event listeners, and POSTing our data
    var oXHR = new XMLHttpRequest();
    oXHR.upload.addEventListener('progress', uploadProgress, false);
    oXHR.addEventListener('load', uploadFinish, false);
    oXHR.addEventListener('error', uploadError, false);
    oXHR.addEventListener('abort', uploadAbort, false);
    var domain_name = "/";
    var wormhole_name = document.getElementById("wormhole_name").innerHTML;
    oXHR.open('POST', domain_name+wormhole_name);
    oXHR.send(vFD);

    // set inner timer
    oTimer = setInterval(doInnerUpdates, 300);
}

function doInnerUpdates() { // we will use this function to display upload speed
    var iCB = iBytesUploaded;
    var iDiff = iCB - iPreviousBytesLoaded;

    // if nothing new loaded - exit
    if (iDiff == 0)
        return;

    iPreviousBytesLoaded = iCB;
    iDiff = iDiff * 2;
    var iBytesRem = iBytesTotal - iPreviousBytesLoaded;
    var secondsRemaining = iBytesRem / iDiff;

    // update speed info
    var iSpeed = iDiff.toString() + 'B/s';
    if (iDiff > 1024 * 1024) {
        iSpeed = (Math.round(iDiff * 100/(1024*1024))/100).toString() + 'MB/s';
    } else if (iDiff > 1024) {
        iSpeed =  (Math.round(iDiff * 100/1024)/100).toString() + 'KB/s';
    }

    document.getElementById('speed').innerHTML = iSpeed;
    document.getElementById('remaining').innerHTML = '| ' + secondsToTime(secondsRemaining);
}

function uploadProgress(e) { // upload process in progress
    if (e.lengthComputable) {
        iBytesUploaded = e.loaded;
        iBytesTotal = e.total;
        var iPercentComplete = Math.round(e.loaded * 100 / e.total);
        var iBytesTransfered = bytesToSize(iBytesUploaded);

        document.getElementById('progress_percent').innerHTML = iPercentComplete.toString() + '%';
        document.getElementById('progress').style.width = (Math.round(iPercentComplete * 2.5)).toString() + 'px';
        document.getElementById('b_transfered').innerHTML = iBytesTransfered;
        if (iPercentComplete == 100) {
            var oUploadResponse = document.getElementById('file_notice');
            oUploadResponse.innerHTML = '正在处理上传数据，请耐心等待';
        }
    } else {
        document.getElementById('progress').innerHTML = 'unable to compute';
    }
}

function uploadFinish(e) { // upload successfully finished

    document.getElementById('progress_percent').innerHTML = '100%';
    document.getElementById('progress').style.width = '250px';
    document.getElementById('remaining').innerHTML = '| 00:00:00';
    
    clearInterval(oTimer);
    var domain_name = "/";
    var wormhole_name = document.getElementById("wormhole_name").innerHTML;
    window.location.href = domain_name+wormhole_name;
}

function uploadError(e) { // upload error
    document.getElementById('file_notice').innerHTML = 'sorry,upload error';
    clearInterval(oTimer);
}

function uploadAbort(e) { // upload abort
    document.getElementById('file_notice').innerHTML = 'sorry,upload aborted';
    clearInterval(oTimer);
}

/**************************** delete file *******************************/
function filedel(fileid) { // delete file
    var domain_name = "/";
    var wormhole_name = document.getElementById("wormhole_name").innerHTML;
    var ip = document.getElementById('user_ip').value;
    $.post(domain_name+wormhole_name,
        {'user_ip':ip,'del_id':fileid},
        function(result){
            document.getElementById('filedel'+fileid).innerHTML = result;
            document.getElementById('collapse'+fileid).innerHTML = "";
        }
    );
    
}
