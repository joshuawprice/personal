use tailcall::tailcall;
use std::io::{self, Write};

#[tailcall]
fn fibonacci(n: u128) -> u128 {
    fn fib_tail(n: u128, a: u128, b: u128) -> u128 {
        if n == 0 {
            a
        } else {
            fib_tail(n - 1, b, a + b)
        }
    }

    fib_tail(n, 0, 1)
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    print!("Enter the fibonacci number you'd like: ");
    io::stdout().flush().unwrap();

    let mut input = String::new();
    let input: u128 = io::stdin().read_line(&mut input).map(|_| input.trim().parse())??;

    println!("{}", fibonacci(input));

    Ok(())
}
