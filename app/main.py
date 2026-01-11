fetch("https://trustlayer-backend-1.onrender.com/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(data)
})

