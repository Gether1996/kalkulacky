import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterLink } from '@angular/router';
import { BlogService } from '../../services/blog.service';
import { BlogCategory, BlogPostSummary } from '../../models/blog.models';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './blog-list.component.html',
  styleUrls: ['./blog-list.component.css']
})
export class BlogListComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  
  categories: BlogCategory[] = [];
  posts: BlogPostSummary[] = [];
  filteredPosts: BlogPostSummary[] = [];
  selectedCategory: string | null = null;
  loading: boolean = true;
  error: string | null = null;

  constructor(private blogService: BlogService) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.loadCategories();
      this.loadPosts();
    }
  }

  loadCategories() {
    this.blogService.getCategories().subscribe({
      next: (data) => {
        this.categories = data;
      },
      error: (err) => {
        console.error('Error loading categories:', err);
      }
    });
  }

  loadPosts(category?: string) {
    this.loading = true;
    this.error = null;
    
    const params = category ? { category } : undefined;
    
    this.blogService.getPosts(params).subscribe({
      next: (data) => {
        this.posts = data;
        this.filteredPosts = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading posts:', err);
        this.error = 'Chyba pri načítavaní blogových príspevkov';
        this.loading = false;
      }
    });
  }

  filterByCategory(categorySlug: string | null) {
    this.selectedCategory = categorySlug;
    if (categorySlug) {
      this.loadPosts(categorySlug);
    } else {
      this.loadPosts();
    }
  }

  getPostUrl(slug: string): string {
    return `/blog/${slug}`;
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('sk-SK', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
}
