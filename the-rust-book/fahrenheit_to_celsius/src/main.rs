use std::io::Write;

fn f_to_c(temp: i32) -> f64 {
    // ((temp - 32) * 5/9).into()
    <i32 as Into<f64>>::into(temp - 32) * 5.0/9.0
}

fn main() {
    println!("Enter a temperature in fahrenheit.");
    print!("> ");
    std::io::stdout().flush().expect("Failed to flush stdout I guess. :shrug:");

    let mut input = String::new();

    std::io::stdin()
        .read_line(&mut input)
        .expect("Failed to readline.");

    let input = input.trim().parse().expect("Failed.");

    let output = f_to_c(input);

    println!("{input} in celsius is: {output}");
}
