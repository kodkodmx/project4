function edit(){
    // console.log("edit");
    var current=document.getElementById("current");
    var edit=document.getElementById("edit");
    current.style.display="none";
    edit.style.display="block";
}

function save(id){
    //console.log(id);
    var current=document.getElementById("current");
    var edit=document.getElementById("edit");
    const new_content=document.getElementById("content").value;
    // console.log(new_content);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(`/edit/${id}`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({
            content:new_content
        })
    })
    .then(response=>response.json())
    .then(result=>{
        // console.log(result);
        document.getElementById("new_content").innerHTML=result.data;
    })

    current.style.display="block";
    edit.style.display="none";
}