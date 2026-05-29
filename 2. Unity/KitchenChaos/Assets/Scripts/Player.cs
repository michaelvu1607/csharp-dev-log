using UnityEngine;
using UnityEngine.InputSystem;

public class Player : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 7f;
    [SerializeField] private float rotSpeed = 15f;
    [SerializeField] private GameInput gameinput;

    private bool isWalking;
    private Vector3 lastInteractDir;
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

        // checks for ClearCounter
        if (Physics.Raycast(transform.position, lastInteractDir, out RaycastHit raycastHit, interactDistance))
        {
            if (raycastHit.transform.TryGetComponent(out ClearCounter clearCounter))
            {
                // has ClearCounter
                clearCounter.Interact();
            }
        }
        else
        {
            Debug.Log("-");
        }
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
}
