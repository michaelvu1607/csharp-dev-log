using UnityEngine;
using UnityEngine.PlayerLoop;

public class Animations : MonoBehaviour
{
    // using constant to reduce human error
    private const string IS_WALKING = "IsWalking";
    
    // reference to the main script to read the Player's state
    private Animator animator;

    [SerializeField] private Player player;
    
    private void Awake()
    {
        // cache animator component attached to this game object
        animator = GetComponent<Animator>();
    }

    private void Update()
    {
        // sync player animator state with player movement state
        animator.SetBool(IS_WALKING, player.IsWalking());
    }
}
