function readURL(input)
{
	if (input.files && input.files[0])
    {
		var reader = new FileReader();
		reader.onload = function(e)
        {
			document.getElementById('preview').src = e.target.result;
			document.getElementById('btn_value').innerHTML = "다시 선택"
			document.getElementById('anal-btn').style= "display: inline-block;"
		};
		reader.readAsDataURL(input.files[0]);
	}
    else
    {
		document.getElementById('preview').src = "https://i0.wp.com/adventure.co.kr/wp-content/uploads/2020/09/no-image.jpg";
	}
}
