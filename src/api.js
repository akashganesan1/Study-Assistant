export const fetchResponse =  async(message) => {
    try {
        // after depoloyment you should change the fetch URL below
        const response = await fetch('http://localhost:5000/get-response', { 
            method: 'POST',
            mode: "cors",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: message
            })
        })

        const data = await response.json()
        return data
    } catch (error) {
        console.log(error);
    }
}
