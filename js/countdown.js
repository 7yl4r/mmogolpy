
var count_down = document.getElementById('countDown');

function uCountdown(){
    
    if( count_down.innerHTML > 0 ){
        count_down.innerHTML = count_down.innerHTML-1;
    }
        
}