function greetings()
{
    let name = document.querySelector('#name').value;
    if (name === " " || name === "")
    {
        alert("Hello, world! Welcome to my page!\nPlease use the navigation on the top to browse through the website!")
    }
    else
    {
        alert("Hello, "+ name +"! Welcome to my page!\nPlease use the navigation on the top to browse through the website!")
    }
}

function QNA()
{
    alert("I am not going to answer actually but as Professor David J. Malan always said, 'A very good question!'")
}