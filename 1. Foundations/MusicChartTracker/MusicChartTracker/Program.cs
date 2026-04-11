using System;
using System.ComponentModel.DataAnnotations;
  
namespace MusicChartTracker
{
    class Program
    {
        // 1. GLOBAL SETTINGS
        // TODO: Create a constant int for MAX_SONGS (set it to 5)
        public const int MAX_SONGS = 5;
        // TODO: Create a static string[] array for songNames with size MAX_SONGS
        private static string[] _songNames = new string[MAX_SONGS];
        // TODO: Create a static string[] array for harmonicKeys with size MAX_SONGS
        private static string[] _harmonicKeys = new string[MAX_SONGS];
        // TODO: Create a static int for currentCount to track how many songs are added
        private static int _currentCount = 0;

        static void Main(string[] args)
        {
            // 2. THE MAIN LOOP
            // TODO: Create a while(true) loop for the menu
            // TODO: Display options: [1] Add Song, [2] View Chart, [3] Exit
            while (true)
            {
                Console.WriteLine("[1] Add Song, [2] View Chart, [3] Exit");
                int input;
                if (!int.TryParse(Console.ReadLine(), out input))
                {
                    Console.WriteLine("Invalid Input");
                    continue;
                }
                switch (input)
                {
                    case 1:
                        AddSong();
                        GetSongsCount();
                        break;
                    case 2:
                        ViewChart();
                        break;
                    case 3:
                        return;
                    default:
                        Console.WriteLine("Please enter a valid number [1|2|3]");
                        break;
                }
            }
            
            // 3. INPUT HANDLING
            // TODO: Use your int.TryParse skills to get the user's menu choice
            
            // 4. THE LOGIC BRANCHES
            // TODO: If choice is 1, call the AddSong() method
            // TODO: If choice is 2, call the ViewChart() method
            // TODO: If choice is 3, break the loop
        }

        // 5. THE ADDING METHOD
        static void AddSong()
        {
            // TODO: Check if currentCount < MAX_SONGS
            if (GetSongsCount() < MAX_SONGS)
            {
                // TODO: Ask for Song Name and Key, then save them into the arrays at the currentCount index
                Console.WriteLine("Enter a Song Name");
                string name = Console.ReadLine();
                Console.WriteLine($"What key is {name} in? ");
                string key = Console.ReadLine();
                
                // TODO: Increment currentCount by 1
                _songNames[_currentCount] = name;
                _harmonicKeys[_currentCount] = key;
                AddSongNum();
            }

        }

        // 6. THE VIEWING METHOD
        static void ViewChart()
        {
            // TODO: Use a for loop to iterate from 0 to currentCount
            for (int i = 0; i < GetSongsCount(); i++)
            {
                // TODO: Print the song name and its key (e.g., "1. Starboy - A Minor")
                Console.WriteLine($"{i + 1}.  {_songNames[i]} --- {_harmonicKeys[i]}");
            }
        }
        
        public static string GetSongsAt(int index)
        {
            if (index >= 0 && index < _currentCount)
            {
                return _songNames[index];
            }
            else
            {
                return "Invalid Selection";
            }
        }

        static void AddSongNum()
        {
            _currentCount++;
        }
        static int GetSongsCount()
        {
            return _currentCount;
        }
    }
}