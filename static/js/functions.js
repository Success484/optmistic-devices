function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
document.addEventListener("DOMContentLoaded", function () {
  // Get CSRF token function
  const csrftoken = getCookie("csrftoken");

  // Event delegation for Add to Cart
  document.body.addEventListener("click", function (e) {
    const cartBtn = e.target.closest(".add-to-cart-btn");
    const updateBtn = e.target.closest(".update-cart");
    const removeBtn = e.target.closest(".remove-item");
    const cartCount = document.querySelector("#cart-count-nav");
    const wishlistBtn = e.target.closest(".add-to-wishlist-btn");
    const removeWishlistBtn = e.target.closest(".remove-from-wishlist");

    // Add to Cart
    if (cartBtn) {
      e.preventDefault();
      const productId = cartBtn.dataset.id;

      fetch(window.DJANGO_URLS.addToCart, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: `product_id=${productId}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            if (cartCount) cartCount.textContent = data.cart_count;
            const countElem = document.querySelector("#cart-count");
            if (countElem) countElem.textContent = data.cart_count;
          } else {
            alert(data.message || "Error adding to cart.");
          }
        })
        .catch((err) => console.error("Error adding to cart:", err));
    }

    // Update quantity
    if (updateBtn) {
      e.preventDefault();
      const productId = updateBtn.dataset.id;
      const action = updateBtn.dataset.action;

      fetch(window.DJANGO_URLS.updateCart, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: `product_id=${productId}&action=${action}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const qtyEl = document.querySelector(`#quantity-${productId}`);
            const totalEl = document.querySelector("#cart-total");

            if (qtyEl) qtyEl.textContent = data.cart[productId].quantity;
            if (totalEl) totalEl.textContent = "₦" + data.total.toFixed(2);
          }
        })
        .catch((err) => console.error("Error in update_cart:", err));
    }

    // Remove item from cart
    if (removeBtn) {
      e.preventDefault();
      const productId = removeBtn.dataset.id;

      fetch(window.DJANGO_URLS.removeCart, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: `product_id=${productId}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const cartCount = document.querySelector("#cart-count-nav");
            if (cartCount)
              cartCount.textContent = Object.keys(data.cart).length;
            const itemRow = document.querySelector(`#cart-item-${productId}`);
            const totalEl = document.querySelector("#cart-total");
            const itemsCountEl = document.querySelector("#cart-items-count");

            if (itemRow) itemRow.remove();
            if (totalEl) totalEl.textContent = "₦" + data.total.toFixed(2);
            if (itemsCountEl)
              itemsCountEl.textContent = `ITEMS ${
                Object.keys(data.cart).length
              }`;
          } else {
            alert(data.message || "Error removing from cart.");
          }
        })
        .catch((err) => console.error("Error in remove_from_cart:", err));
    }

    // Add to Wishlist
    if (wishlistBtn) {
      e.preventDefault();
      const productId = wishlistBtn.dataset.id;

      fetch(window.DJANGO_URLS.addToWishlist, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: `product_id=${productId}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const wishlistCount = document.querySelector("#wishlist-count-nav");
            if (wishlistCount) wishlistCount.textContent = data.wishlist_count;
          } else {
            alert(data.message);
          }
        })
        .catch((err) => console.error("Error adding to wishlist:", err));
    }

    // Remove from Wishlist
    if (removeWishlistBtn) {
      e.preventDefault();
      const productId = removeWishlistBtn.dataset.id;

      fetch(window.DJANGO_URLS.removeWishlist, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: `product_id=${productId}`,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            // Remove the item from the DOM
            const itemRow = document.querySelector(
              `#wishlist-item-${productId}`
            );
            if (itemRow) itemRow.remove();

            // Update wishlist count in navbar
            const wishlistCount = document.querySelector("#wishlist-count-nav");
            if (wishlistCount) wishlistCount.textContent = data.wishlist_count;

            // Optionally update wishlist count on page (if exists)
            const pageCount = document.querySelector("#wishlist-count");
            if (pageCount)
              pageCount.textContent = `${
                Object.keys(data.wishlist).length
              } items`;
          } else {
            alert(data.message || "Error removing from wishlist.");
          }
        })
        .catch((err) => console.error("Error removing from wishlist:", err));
    }
  });
});
