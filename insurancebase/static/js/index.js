function postFile(event) {
    event.preventDefault();
    const input = document.getElementById('file-input');
    const file = input.files[0];
    const fileType=file.type;
    const formData = new FormData();
    formData.append('file', file);
    const options = {
      method: 'POST',
      body: formData
    };
    fetch('http://3.139.167.247:5000/', options)
      .then(response => response)
      .then(response => {
        console.log(response)
        const output = document.getElementById('output');
        if (response.status===200){
        output.textContent ="Status:"+ response.status+" a "+fileType+"  is uploaded";
        }
        else if (file===undefined){
            output.textContent="Please select a file"
        }
      })
      .catch(error => {
        console.error('Error uploading file:', error);
      });
  }