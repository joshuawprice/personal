fn main() {
    let twelve_gifts: [&str; 12] = [
        "A partridge in a pear tree",
        "Two turtle doves",
        "Three French hens",
        "Four calling birds",
        "Five gold rings",
        "Six geese a-laying",
        "Seven swans a-swimming",
        "Eight maids a-milking",
        "Nine ladies dancing",
        "Ten lords a-leaping",
        "Eleven pipers piping",
        "Twelve drummers drumming",
    ];

    for i in 0..twelve_gifts.len() {
        println!("On the first day of Christmas my true love sent to me");
        for j in (0..=i).rev() {
            if i != 0 && j == 0 {
                println!("And {}", twelve_gifts[0].to_lowercase());
                continue;
            }
            println!("{},", twelve_gifts[j]);
        }
        println!();
    }

    // let mut song_builder = String::from("And a partridge in a pear tree");

    // for i in 0..twelve_gifts.len() {
    //     println!("On the first day of Christmas my true love sent to me");
    //     if i == 0 {
    //         println!("{}", twelve_gifts[0]);
    //     } else {
    //         song_builder = twelve_gifts[i].to_owned() + ",\n" + &song_builder;
    //         println!("{}", song_builder);
    //     }
    //     println!();
    // }
}
