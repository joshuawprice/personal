use std::fs::File;
use std::io::{BufReader, prelude::*};
use std::path::Path;

type Result<T, E = Box<dyn std::error::Error>> = std::result::Result<T, E>;

fn challenge_1() -> Result<i32> {
    let path = Path::new("input.txt");
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let mut total: i32 = 0;
    for line in reader.lines() {
        let line = line?;

        // There are no zeroes in the dataset.
        let mut left_digit = 0;
        let mut right_digit = 0;

        for digit in line.bytes().take(line.as_bytes().len() - 1) {
            if digit > left_digit {
                left_digit = digit;
                right_digit = 0;
            } else if digit > right_digit {
                right_digit = digit;
            }
        }

        if right_digit < line.bytes().last().unwrap() {
            right_digit = line.bytes().last().unwrap();
        }
        // Subtract 48 from the ascii value to get the real number.
        total += ((left_digit - 48) * 10 + (right_digit - 48)) as i32;
    }

    Ok(total)
}

fn main() -> Result<()> {
    println!("Challenge 1: {}", challenge_1()?);

    Ok(())
}

// Naïve way:
// - Search through entire line (except last number as we may need that for the second digit.)
// - Get first highest number in that line.
// - Search through the rest of the line for the highest number again for the second digit.
// - Get first highest number in that slice.
//
//
// Proper(?) way:
// - The goal is to only look at every element in the array once.
// - Iterate through line.
// - Iterating through the list of numbers, stopping at second last digit (see special case):
// - On found number that's higher than leftmost, store, and remove stored less significant digits.
// - On found number ≤ stored leftmost digit and > than stored right digit, put in right digit.
//
// Special case: If highest leftmost digit is second last digit in line
//               (i.e. we reached the end of the loop with no second digit)
// - Fill in the blanks sequentially; there is no more space for searching.
