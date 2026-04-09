/*
 * The Drill: Create an interface called Door.
 * Create three different classes (e.g., Switch, BlastDoor, Terminal) that all implement Door differently.
 * Create a list of these objects and loop through them, triggering their specific interactions.
 */
 
 using IInteractable;

Switch switch1 = new Switch();
Key key1 = new Key();
BlastDoor blastdoor = new BlastDoor(switch1, key1);
Terminal terminal = new Terminal(switch1, key1, blastdoor);

blastdoor.Interact();
terminal.Interact();

Console.WriteLine("");
switch1.ChangeLockedState();
blastdoor.Interact();
terminal.Interact();

Console.WriteLine("");
key1.ChangeLockedState();
blastdoor.Interact();
terminal.Interact();

Console.WriteLine("");
switch1.ChangeLockedState();
key1.ChangeLockedState();
blastdoor.Interact();
terminal.Interact();