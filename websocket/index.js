var ws = new WebSocket("ws://127.0.0.1:8000")
ws.binaryType = "arraybuffer"
let audiocontext
let audiodata
let rec


var recordRTC = null;
ws.addEventListener("message", (event) => {
    audiocontext.decodeAudioData(event.data).then(
        decodedaudio =>{
            audiodata = decodedaudio
            const playSound = audiocontext.createBufferSource();
            playSound.buffer = audiodata;
            playSound.connect(audiocontext.destination);
            playSound.start(audiocontext.currentTime);
        }
    )
});

var call = document.getElementById("call")
// button.onclick = function(){
//     audiocontext = new AudioContext()
//     ws.send("hi")
// }

const constraints = {
    audio: true,
    video:false
};
function onError(err){
    console.log(err)
}




call.onclick = function(){
    audiocontext = new AudioContext()
    ws.send("hi")

}

let digits = document.getElementsByClassName("digit")
for(let i = 0;i<digits.length;i++){
    digits[i].addEventListener('click',function(){
        if(digits[i].innerText.split("\n")[0] == 1 || digits[i].innerText.split("\n")[0] == 2 || digits[i].innerText.split("\n")[0] == 3){
            ws.send(parseInt(digits[i].innerText.split("\n")[0]))
            makecall()
        }


    })
}

const stopRecordButton = document.getElementById('end-call');

async function makecall(){
    console.log('z')
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    recorder.start();
    recorder.addEventListener("dataavailable", async (event) => {
        // Write chunks to the file.
        console.log('hi')
        
         ws.send(event.data);
        // if (recorder.state === "inactive") {
        //   // Close the file when the recording stops.
        //   await writable.close();
        // }
    
      });
}

stopRecordButton.addEventListener("click", () => {
    // Stop the recording.
    recorder.stop();
});
