use std::collections::HashMap;

fn main() {
    // Badly shuffled fibonacci sequence.
    let mut vec = vec![0, 89, 1, 55, 1, 34, 2, 21, 3, 13, 5, 8, 144];
    // let mut vec = vec![0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144];

    // Sort the vecotr so that we can compute the median later.
    vec.sort_unstable();

    // Compute and print median.
    println!("Median: {}", vec.get(vec.len() / 2).copied().unwrap_or_default());


    // Count most common value in vector.
    let mut hashmap = HashMap::new();
    for i in vec {
        *hashmap.entry(i).or_insert(0) += 1;
    }

    // Now get the mode.
    let mut mode = (&0, &0);
    for i in hashmap.keys() {
        if hashmap.get(i).expect("Getting from previously obtained key.") > mode.1 {
            mode = hashmap.get_key_value(i).expect("Getting from preiously obtained key");
        }
    }

    println!("Mode: {}", mode.0);
}
