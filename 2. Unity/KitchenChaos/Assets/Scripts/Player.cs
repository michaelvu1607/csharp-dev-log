using UnityEngine;
using UnityEngine.InputSystem;

public class Player : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 7f;
    [SerializeField] private float rotSpeed = 15f;
    [SerializeField] private GameInput gameinput;

    private bool isWalking;
    private void Update()
    {
        Vector2 inputVector = gameinput.GetMovementVectorNormalized();
        
        Vector3 moveDir = new Vector3(inputVector.x, 0f, inputVector.y);

        float moveDistance = moveSpeed * Time.deltaTime;
        float playerRadius = .7f;
        float playerHeight = 2f;
        bool canMove = !Physics.CapsuleCast(transform.position, transform.position + Vector3.up * playerHeight, playerRadius, moveDir, moveDistance);

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
        
        if (canMove)
        {
            transform.position += moveDir * moveDistance;

        }

        transform.forward = Vector3.Slerp(transform.forward, moveDir, Time.deltaTime * rotSpeed);

        isWalking = moveDir != Vector3.zero;

        
        Debug.Log(inputVector);
    }

    public bool IsWalking()
    {
        return isWalking;
    }
}
