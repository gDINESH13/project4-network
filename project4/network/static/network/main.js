var csrftoken="";
var currentDate = new Date();
var months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]


document.addEventListener('DOMContentLoaded',load);

function load()
{
	
	document.querySelectorAll('#likepost').forEach(post=>{
		post.addEventListener('click',event=>{likepost(post)});
	});
	if (document.querySelector('#edit'))
	{
	    document.querySelectorAll('#edit').forEach(but=>{
	    	but.onclick=()=>button(but);
	    });
    }
	csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;
}
function button(but)
{
	//alert('button');
	//let but=document.querySelector('#edit');
	if (but.innerHTML=="Edit")
	{
	let m=but.getAttribute('data-id');
	//alert(`${m}`);
	var y=document.querySelector(`#content${m}`).querySelector("h6");
	var tex1=y.textContent;
	//alert(`${tex1}`);
	document.querySelector(`#content${m}`).style.display='none';
	document.querySelector(`#editpost${m}`).style.display="block";
	
	var text=document.querySelector(`#editpost${m}`).querySelector('textarea');
	text.innerHTML=tex1;
	but.innerHTML="save";
	}
	else if(but.innerHTML=="save")
	{
		let m=but.getAttribute('data-id');
		var editpost=document.querySelector(`#editpost${m}`)
		var text=document.querySelector(`#editpost${m}`).querySelector('textarea');
		var new_text=text.value;
		console.log(new_text);
		fetch(`/editpost/${m}`,{
			method:'POST',
			headers:{
				"X-CSRFToken":csrftoken,
				"Accept":"application/json; charset=utf-8",
				"Content-Type": "application/json; charset=utf-8",
				'X-Requested-With': 'XMLHttpRequest'
			},
			body:JSON.stringify({
				new_text:new_text
			})
		})
		.then(response=>response.json())
		.then(result=>
		{
			editpost.style.display="none";
			

			var date = currentDate.getDate();
			var month = currentDate.getMonth(); //Be careful! January is 0 not 1
			var year = currentDate.getFullYear();
			var timestamp =currentDate.getTime();
			document.querySelector(`#content${m}`).style.display='block';
			document.querySelector(`#content${m}`).querySelector("h6").innerHTML=result.content;
			//document.querySelector(`#content${m}`).querySelector("li").innerHTML= months[month ]+ "." + date + " " +"," + year+" "+timestamp;
			document.querySelector(`#content${m}`).querySelector("li").innerHTML=currentDate.toLocaleString();
			console.log(result);
		})
		but.innerHTML="Edit";


	}

}
function likepost(post)
{
	let c=(post.id);
	//alert(`${post.id}`);
	let v=post.getAttribute('data-id');
	//alert(`${v}`);
	var like=false;
	if(post.style.color!="blue")
	{
		like=true;
		post.style.color="blue";
	}
	else
	{
		//like=false;
		post.style.color="black";
	}
	fetch('/likepost',{
		method:'POST',
		headers:{
			"X-CSRFToken":csrftoken,
			"Accept":"application/json; charset=utf-8",
			"Content-Type": "application/json; charset=utf-8",
			'X-Requested-With': 'XMLHttpRequest'
		},
		body:JSON.stringify({
			id:v,
			like:like
		})

	})
	.then(response=>response.json())
	.then(result=>{
		document.querySelector(`#totallikes${v}`).innerHTML = `(${parseInt(result.totallikes)})`;
		console.log(result); 
		
	});
}