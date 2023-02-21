<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
</head>
<body>
    <div class="content">
        <div class="row mb-3">
            <div class="col-2 mt-2 me-1">
                <img src="images/koogle.png" alt="koogle" width="200" height="100">
            </div>
            <div class="col-7 mt-3 ms-4 me-5">
                <div class="input-group mb-3 mt-4" >
                    <input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="basic-addon2">
                    <div class="input-group-append ml-2">
                      <button class="btn btn-outline-secondary" type="button">Search</button>
                    </div>
                  </div>
            </div>
            <div class="col-2 mt-2 ms-5 mt-5">
                <i class="fa-solid fa-gear fa-xl me-4"></i>
                <i class="fas fa-bars fa-xl me-4"></i>
                <button type="button" class="btn btn-secondary btn-rounded btn-icon">
                    <i class="fa fa-user"></i>
                  </button>
            </div>
        </div> 
        
         <?php
         $conex=mysqli_connect("localhost","root","","motor");
         if ($conex->connect_error) {
            die("Connection failed: " . $conex->connect_error);
          }
          echo "Connected successfully";
         $consulta="SELECT * FROM enlaces";
         $resultado=mysqli_query($conex,$consulta);
         if(!empty($resultado) AND mysqli_num_rows($resultado) > 0){
             echo
             "<tr>
             <th>Número de autobús</th>
             <th>Capacidad</th>
             <th>Capacidad</th>
             </tr>";
         while($mostrar=mysqli_fetch_array($resultado)){
         ?>
         <tr>
             <td><?php echo $mostrar['url'] ?></td>
             <td><?php echo $mostrar['titulo'] ?></td>
             <td><?php echo $mostrar['contenido'] ?></td>
         </tr>
         <?php
         }
         }else{
             echo "<h3 style='text-align:center'>No hay registros almacenados</h3>";
         }
         ?>
    </div>
</body>
  <!--Bootstrap-->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.min.js" integrity="sha384-IDwe1+LCz02ROU9k972gdyvl+AESN10+x7tBKgc9I5HFtuNz0wWnPclzo6p9vxnk" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
  <!--FontAwesome-->
  <script src="https://kit.fontawesome.com/fe7b30889a.js" crossorigin="anonymous"></script>
</html>