const searchForm = document.querySelector('[form-search]')
if (searchForm) {
  searchForm.addEventListener('click', () => {
    const searchHeader = document.querySelector('[header-search]')
    searchHeader.classList.toggle('d-block')
  })
}

const cartNumber = document.querySelector("#cart_quantity")
if (cartNumber) {
  const number = cartNumber.textContent
  if (number == 0) {
    cartNumber.classList.add('d-none')
  }
}



const productHover = document.querySelector('.spdd-hover')
if (productHover) {
  const productDD = document.querySelector('.productdd-container')
  productHover.addEventListener('mouseover', () => {
    productDD.classList.remove('hide')
    productDD.classList.add('show')
  })
  productHover.addEventListener('mouseout', () => {
    productDD.classList.remove('show')
    productDD.classList.add('hide')
  })
}

const collectionHover = document.querySelector('.bstdd-hover')
if (collectionHover) {
  const collectionDD = document.querySelector('.bstdd-container')
  collectionHover.addEventListener('mouseover', () => {
    collectionDD.classList.remove('hide')
    collectionDD.classList.add('show')
  })
  collectionHover.addEventListener('mouseout', () => {
    collectionDD.classList.remove('show')
    collectionDD.classList.add('hide')
  })
}

