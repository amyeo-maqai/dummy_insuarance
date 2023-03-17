let postFile=async (event)=> {
  event.preventDefault();
  const input = document.getElementById('file-input');
  const file = input.files[0];
  const fileType = file.type;
  const formData = new FormData();
  let spinnerEl = document.getElementById('spinner');
  spinnerEl.classList.remove("d-none");
  formData.append('file', file);
  const options = {
    method: 'POST',
    body: formData
  };

  try {
    const response=await fetch('http://3.139.167.247:5000/fileupload/', options)
      .then(response => response.json())
      .then(data => {
        console.log(typeof data)
        // console.log(response.json())
        const output = document.getElementById('output');
        spinnerEl.classList.add("d-none");
        if (data.status === 200) {
          output.textContent = "Result:" + data.message
        }
        else {
          output.textContent = "Please select a file"
        }
      })
      .catch(error => {
        // console.log(error)
        // console.log(error.message)
        spinnerEl.classList.add("d-none");
        output.textContent = "Failed To Upload"
      });
  }
  catch(error){
    console.log(error.message)
  }
}