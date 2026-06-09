using UnityEngine;


public class ClearCounter : BaseCounter
{
    [SerializeField] private KitchenObjectSO kitchenObjectSO;

    public override void Interact(Player player)
    {
        if (!HasKitchenObject())
        {
            // counter not occupied by item
            if (player.HasKitchenObject())
            {
                // player  carrying item
                player.GetKitchenObject().SetKitchenObjectParent(this);
            }
            else
            {
                // player not carrying item
            }
        }
        else
        {
            // counter occupied by item
            if (player.HasKitchenObject())
            {
                // player carrying item
            }
            else
            {
                // player not carrying item
                GetKitchenObject().SetKitchenObjectParent(player);
            }
        }
    }
}
