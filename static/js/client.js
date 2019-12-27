var img1 = document.getElementById("liveImg1");
var img2 = document.getElementById("liveImg2");
var arrayBuffer1;
var arrayBuffer2;

// var camSocketws = new WebSocket('ws://' + document.location.host + '/camera');
// ws.binaryType = 'arraybuffer';

// ws.onopen = function(){
//     console.log("connection was established");
// };
// ws.onmessage = function(evt){
//     console.log("receive message")
//     arrayBuffer = evt.data;
//     img.src = "data:image/jpeg;base64," + encode(new Uint8Array(arrayBuffer));
// };

var camSocket1 = new WebSocket('ws://' + document.location.host + '/cam_server1');
camSocket1.binaryType = 'arraybuffer';

camSocket1.onopen = function(){
    console.log("connection was established 1");
};
camSocket1.onmessage = function(evt){
    console.log("receive message 1")
    arrayBuffer1 = evt.data;
    img1.src = "data:image/jpeg;base64," + encode(new Uint8Array(arrayBuffer1));
};


var camSocket2 = new WebSocket('ws://' + document.location.host + '/cam_server2');
camSocket2.binaryType = 'arraybuffer';

camSocket2.onopen = function(){
    console.log("connection was established 2");
};
camSocket2.onmessage = function(evt){
    console.log("receive message 2")
    arrayBuffer2 = evt.data;
    img2.src = "data:image/jpeg;base64," + encode(new Uint8Array(arrayBuffer2));
};


function encode (input) {
    var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var output = "";
    var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
    var i = 0;

    while (i < input.length) {
        chr1 = input[i++];
        chr2 = i < input.length ? input[i++] : Number.NaN; // Not sure if the index
        chr3 = i < input.length ? input[i++] : Number.NaN; // checks are needed here

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
            enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
            enc4 = 64;
        }
        output += keyStr.charAt(enc1) + keyStr.charAt(enc2) +
                  keyStr.charAt(enc3) + keyStr.charAt(enc4);
    }
    return output;
}