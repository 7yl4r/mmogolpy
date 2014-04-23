<script type="text/javascript">

    var R{{row}}C{{col}} = document.getElementById('R{{row}}C{{col}}');

    R{{row}}C{{col}}.addEventListener('click', function (e)
    {
        e = e || window.event; //? what is this?

        R{{row}}C{{col}}.style.color = "rgb(100,200,255)";
        R{{row}}C{{col}}.innerHTML = (1-R{{row}}C{{col}}.innerHTML);
       // R{{row}}C{{col}}.style.class = "local-change"; // NOTE: couldn't get this to work right, but using classes would be better.
        console.log("{{row}},{{col}} clicked");
        ws.send("set {{row}} {{col}} " + R{{row}}C{{col}}.innerHTML);

        e.preventDefault(); //? what is that?
    }, false);
    
</script>