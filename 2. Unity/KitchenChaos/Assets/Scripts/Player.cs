using System;
using UnityEngine;
using UnityEngine.InputSystem;

public class Player : MonoBehaviour
{
    // Singleton Pattern: allows visual scripts to find Player and subscribe to it
    public static Player Instance { get; private set; }
    
    // broadcast tower for when Player's line of site changes
    public event EventHandler<OnSelectedCounterChangedEventArgs> OnSelectedCounterChanged;

    public class OnSelectedCounterChangedEventArgs : EventArgs
    {
        public ClearCounter selectedCounter;
    }
    
    [SerializeField] private float moveSpeed = 7f;
    [SerializeField] private float rotSpeed = 15f;
    [SerializeField] private GameInput gameinput;
    [SerializeField] private LayerMask counterLayerMask;

    private bool isWalking;
    private Vector3 lastInteractDir;
    private ClearCounter selectedCounter;

    private void Awake()
    {
        if (Instance != null)
        {
            Debug.LogError("There is more than one player instances on the scene!");
        }
        else
        {
            Instance = this;
        }
    }

    private void Start()
    {
        // Player subscribes to GameInput's broadcast tower
        gameinput.OnInteractAction += GameInputOnInteractAction;
    }

    // executes immediately after Interact button is pressed
    private void GameInputOnInteractAction(object sender, EventArgs e)
    {
        if (selectedCounter != null)
        {
            selectedCounter.Interact();
        }
    }

    private void Update()
    {
        HandleMovement();
        HandleInteractions();
    }
    
    // used in PlayerAnimator.Update() to change animation state when player is idle/walking
    public bool IsWalking()
    {
        return isWalking;
    }

    private void HandleInteractions()
    {
        // gets moveDir unaffected by blocked movement direction in HandleMovement()
        Vector2 inputVector = gameinput.GetMovementVectorNormalized();
        Vector3 moveDir = new Vector3(inputVector.x, 0f, inputVector.y);
        
        // gets direction player is facing
        if (moveDir != Vector3.zero)
        {
            lastInteractDir = moveDir;
        }

        float interactDistance = 2f;

        // checks for objects in front of player
        if (Physics.Raycast(transform.position, lastInteractDir, out RaycastHit raycastHit, interactDistance, counterLayerMask))
        {
            // checks if object is a ClearCounter (has ClearCounter script attached)
            if (raycastHit.transform.TryGetComponent(out ClearCounter clearCounter))
            {
                // checks to see which clearCounter Player is facing
                if (clearCounter != selectedCounter)
                {
                    SetSelectedCounter(clearCounter);
                }
            }
            else
            {
                SetSelectedCounter(null);
            }
        }
        else
        {
            SetSelectedCounter(null);
        }
        
        Debug.Log(selectedCounter);
    }
    private void HandleMovement()
    {
        // flattens the 2D input vector onto the 3D plane
        Vector2 inputVector = gameinput.GetMovementVectorNormalized();
        Vector3 moveDir = new Vector3(inputVector.x, 0f, inputVector.y);
        
        // defines the dimensions of the player's surrounding for collision detection
        float playerRadius = .7f;
        float playerHeight = 2f;
        float moveDistance = moveSpeed * Time.deltaTime;

        // cast a capsule to project if the player will collide with an obstacle
        bool canMove = !Physics.CapsuleCast(transform.position, transform.position + Vector3.up * playerHeight, playerRadius, moveDir, moveDistance);

        // if direct movement is blocked, handle sliding by checking individuals axes independently
        if (!canMove)
        {
            // Attempt X
            Vector3 moveDirX = new Vector3(moveDir.x, 0, 0).normalized;
            canMove = !Physics.CapsuleCast(transform.position, transform.position + Vector3.up * playerHeight, playerRadius, moveDirX, moveDistance);
           
            if (canMove)
            {
                // Can only move X
                moveDir = moveDirX;
            }
            
            else
            {
                // Attempt Z
                Vector3 moveDirZ = new Vector3(0, 0, moveDir.z).normalized;
                canMove = !Physics.CapsuleCast(transform.position, transform.position + Vector3.up * playerHeight, playerRadius, moveDirZ, moveDistance);
                
                if (canMove)
                {
                    // Can only move Z
                    moveDir = moveDirZ;
                }
                
                else
                {
                    // Cannot move in any direction
                }
            }
        }
        
        // execute movement is path is clear (direct or sliding)
        if (canMove)
        {
            transform.position += moveDir * moveDistance;

        }

        // smoothly interpolate player's rotation to face direction of movement
        transform.forward = Vector3.Slerp(transform.forward, moveDir, Time.deltaTime * rotSpeed);

        // evaluate movement state to change animation
        isWalking = moveDir != Vector3.zero;
    }
    
    private void SetSelectedCounter(ClearCounter selectedCounter)
    {
        // sets the selectedCounter to another clearCounter or null
        this.selectedCounter = selectedCounter;
        
        // broadcasts the event to subscribers (SelectedCounterVisuals) with custom EventArgs
        OnSelectedCounterChanged?.Invoke(this, new OnSelectedCounterChangedEventArgs {selectedCounter = selectedCounter});
    }
}
