
import random
from pynput.keyboard import Key, Listener
import itertools


# we want to take an arbitrary list, make a number of comparisons until we get bored, then sort the final thing by elo

# create a listener to check if the left or right arrow keys are pressed
def on_press(key):
    global left_key_pressed
    global right_key_pressed
    try:
        # Check if the key is either the left or right arrow key
        if key == Key.left:
            left_key_pressed = True
        elif key == Key.right:
            right_key_pressed = True
        else:
            return True
        return False
    except AttributeError:
        pass #stop the listener

def sample_pairs(lst, num_comparisons):
    # Generate all unique pairs from the list
    all_pairs = list(itertools.combinations(lst, 2))
    
    # Shuffle the pairs to ensure randomness
    random.shuffle(all_pairs)
    
    # Return the first X pairs
    if num_comparisons > len(all_pairs):
        return all_pairs
    else:
        return all_pairs[:num_comparisons]



def compare_and_update(a, b, winner, elos, k):
    a_elo = elos[a]
    b_elo = elos[b]
    a_win = 0
    b_win = 0
    # expected probability of winning
    a_expected = 1 / (1 + 10 ** ((b_elo - a_elo) / 400))
    b_expected = 1 / (1 + 10 ** ((a_elo - b_elo) / 400))

    if winner == a:
        a_win = 1
    elif winner == b:
        b_win = 1
    else:
        raise TypeError("Winner value must be equivalent to A or B")
    elos[a] = int(a_elo + k * (a_win - a_expected))
    elos[b] = int(b_elo + k * (b_win - b_expected))


def main(list_of_items, num_comparisons,k=100):
    # all elos should be 1k originally
    return "<p>hello world</p>"
    elos = {x: 1000 for x in list_of_items}

    # get a list of pairs
    pairs = sample_pairs(list_of_items, num_comparisons)

    for pair in pairs:
        a, b = pair

        left_key_pressed,right_key_pressed = False,False
        print(f"Which is better? {a} or {b}. \n\n {a} <----, ----> {b}")
        # Create a keyboard listener
        with Listener(on_press=on_press) as listener:
            listener.join()

        winner = a if left_key_pressed else b

        compare_and_update(a,b,winner,elos,k)

    # sort the list by elo
    sorted_list = sorted(elos.items(), key=lambda x: x[1], reverse=True)

    final_list = [x[0] for x in sorted_list]
    return final_list


# decide on a method to get the original list
taylor_swift_albums = ["Taylor Swift", "Fearless (not TV)", "Speak Now (not TV)", "Red (not TV)", "1989", "Reputation", "Lover", "Folklore", "Evermore", "Midnights", "Red (TV)"]
 # we need to set a k value that determines how much elo is gained/lost per comparison
# changing this makes it more or less volatile
k = 200

num_comparisons = 10

print(main(taylor_swift_albums, num_comparisons, k))