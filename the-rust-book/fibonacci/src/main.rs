use std::io;
use std::io::Write;

fn main() {
    println!("Which number in the fibonacci sequence would you like to generate?");
    print!("> ");
    std::io::stdout().flush().expect("Failed to flush stdout.");

    loop {
        let mut n = String::new();

        io::stdin()
            .read_line(&mut n)
            .unwrap();
        
        let n: usize = match n.trim().parse() {
            Ok(num) => num,
            Err(_) => continue
        };


        let mut fib_cache: [i128; 2] = [0, 1];

        for i in 0..n {
            fib_cache[i % 2] = fib_cache[0] + fib_cache[1];
        }
        println!("{}", fib_cache[n % 2]);
        break;
    }

}
