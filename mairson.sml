(* pathological example from Mairson *)
structure P = struct

fun main _ = 0

val wat = fn _ =>
   let val x1 = (fn y => fn z => z y y)
   in let val x2 = (fn y => x1(x1(y)))
      in let val x3 = (fn y => x2(x2(y)))
         in let val x4 = (fn y => x3(x3(y)))
            in
               x4
            end
         end
      end
   end

end

(* 
up to x4:
utahraptor:bangbangcon aki$ /usr/bin/time ml-build pathological.cm P.main ;
...
[code: 164340, env: 269 bytes]
...
[code: 445, data: 41, env: 40 bytes]
        2.46 real         1.84 user         0.55 sys

up to x5:
utahraptor:bangbangcon aki$ /usr/bin/time ml-build pathological.cm P.main ;
...
[code: 37667020, env: 438 bytes]
...
[code: 445, data: 41, env: 40 bytes]
    32259.10 real     24709.07 user      6906.16 sys
*)
