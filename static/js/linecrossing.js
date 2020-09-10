$(document).ready(function(){
    // console.log(data)
    const cams = []
    for(let i=1; i <= data.length; i++){
        let ref = firebase.database().ref(`line Crossing/cam${i}`);
        ref.once("value")
            .then(function(snapshot) {
               if(snapshot.hasChild("configuration")){
                   cams.push(snapshot.val())
               } // true)
                // var hasAge = snapshot.hasChild("age"); // false
            });
    }
    $('#configBtn').on('click', function(){
        fetch('/run-configuration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(resp => {
            return resp.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch(err => {
            console.log(err);
        })
    })
    
    
})