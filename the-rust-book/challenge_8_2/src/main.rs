use std::io::{self, Write};

const VOWELS: &str = "aeiou";

fn main() {
    loop {
        let mut user_input = String::new();

        println!("Please input some words.");
        print!("> ");
        io::stdout()
            .flush()
            .expect("Failed to flush stdout buffer.");

        io::stdin()
            .read_line(&mut user_input)
            .expect("Failed to read input.");

        let mut new_string = String::new();
        for word in user_input.split_whitespace() {
            // Save iterator for use when word begins with consonant.
            let mut word_iter = word.chars();
            let first_letter = word_iter.next().expect("Failed to get first letter.");

            if VOWELS.contains(first_letter) {
                new_string.push_str(&format!("{word}-hay"));
            } else {
                new_string.push_str(&format!("{}-{}ay", word_iter.as_str(), first_letter));
            }
            new_string.push(' ');
        }

        println!("{new_string}");
    }
}
